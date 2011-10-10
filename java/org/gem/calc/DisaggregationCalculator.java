package org.gem.calc;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.apache.commons.collections.Closure;
import org.opensha.commons.data.Site;
import org.opensha.commons.data.function.DiscretizedFuncAPI;
import org.opensha.commons.geo.Location;
import org.opensha.commons.geo.LocationList;
import org.opensha.commons.geo.LocationUtils;
import org.opensha.sha.earthquake.EqkRupForecastAPI;
import org.opensha.sha.earthquake.ProbEqkRupture;
import org.opensha.sha.earthquake.ProbEqkSource;
import org.opensha.sha.earthquake.rupForecastImpl.GEM1.GEM1ERF;
import org.opensha.sha.imr.ScalarIntensityMeasureRelationshipAPI;
import org.opensha.sha.util.TectonicRegionType;
import static org.apache.commons.collections.CollectionUtils.forAllDo;

public class DisaggregationCalculator {

	private final Double[] latBinLims;
	private final Double[] lonBinLims;
	private final Double[] magBinLims;
	private final Double[] epsilonBinLims;
	private final Double[] distanceBinLims;
	private static final TectonicRegionType[] tectonicRegionTypes = TectonicRegionType.values();

	/**
	 * Used for checking that bin edge lists are not null;
	 */
	private static final Closure notNull = new Closure()
	{

		public void execute(Object o)
		{
			if (o == null)
			{
				throw new IllegalArgumentException("Bin edges should not be null");
			}
		}
	};

	/**
	 * Used for checking that bin edge lists have a length greater than or equal
	 * to 2.
	 */
	private static final Closure lenGE2 = new Closure()
	{

		public void execute(Object o)
		{
			if (o instanceof Object[])
			{
				Object[] oArray = (Object[]) o;
				if (oArray.length < 2)
				{
					throw new IllegalArgumentException("Bin edge arrays must have a length >= 2");
				}
			}
		}
	};

	private static final Closure isSorted = new Closure()
	{

		public void execute(Object o) {
			if (o instanceof Object[])
			{
				Object[] oArray = (Object[]) o;
				Object[] sorted = Arrays.copyOf(oArray, oArray.length);
				Arrays.sort(sorted);
				if (!Arrays.equals(sorted, oArray))
				{
					throw new IllegalArgumentException("Bin edge arrays must arranged in ascending order");
				}
			}
		}
	};

	public DisaggregationCalculator(
			Double[] latBinEdges,
			Double[] lonBinEdges,
			Double[] magBinEdges,
			Double[] epsilonBinEdges,
			Double[] distanceBinEdges)
	{
		List binEdges = Arrays.asList(latBinEdges, lonBinEdges, magBinEdges,
				  epsilonBinEdges, distanceBinEdges);

		// Validation for the bin edges:
		forAllDo(binEdges, notNull);
		forAllDo(binEdges, lenGE2);
		forAllDo(binEdges, isSorted);

		this.latBinLims = latBinEdges;
		this.lonBinLims = lonBinEdges;
		this.magBinLims = magBinEdges;
		this.epsilonBinLims = epsilonBinEdges;
		this.distanceBinLims = distanceBinEdges;
	}

	public double[][][][][] computeMatrix(
			Site site,
			GEM1ERF erf,
			Map<TectonicRegionType, ScalarIntensityMeasureRelationshipAPI> imrMap,
			double poe,
			DiscretizedFuncAPI hazardCurve) // or just pass a List<double> of IML values and compute the curve inside here?
	{
		double disaggMatrix[][][][][] =
				new double[latBinLims.length - 1]
						  [lonBinLims.length - 1]
						  [magBinLims.length - 1]
						  [epsilonBinLims.length - 1]
						  [tectonicRegionTypes.length];
		
		// value by which to normalize the final matrix
		double totalAnnualRate = 0.0;

		double minMag = (Double) erf.getParameter(GEM1ERF.MIN_MAG_NAME).getValue();
		double gmv = 0.0;  // TODO calculate me
		
		for (int srcCnt = 0; srcCnt < erf.getNumSources(); srcCnt++)
		{
			ProbEqkSource source = erf.getSource(srcCnt);

			double totProb = source.computeTotalProbAbove(minMag);
			double totRate = -Math.log(1 - totProb);

			TectonicRegionType trt = source.getTectonicRegionType();

			ScalarIntensityMeasureRelationshipAPI imr = imrMap.get(trt);
			imr.setSite(site);
			imr.setIntensityMeasureLevel(gmv);

			for(int rupCnt = 0; rupCnt < source.getNumRuptures(); rupCnt++)
			{
				ProbEqkRupture rupture = source.getRupture(rupCnt);
				imr.setEqkRupture(rupture);

				Location location = closestLocation(rupture.getRuptureSurface().getLocationList(), site.getLocation());

				double lat, lon, mag, epsilon;
				lat = location.getLatitude();
				lon = location.getLongitude();
				mag = rupture.getMag();
				epsilon = imr.getEpsilon();

				if (!allInRange(lat, lon, mag, epsilon))
				{
					// one or more of the parameters is out of range;
					// skip this rupture
					continue;
				}

				int[] binIndex = getBinIndices(lat, lon, mag, epsilon, trt);

				double annualRate = totRate
						* imr.getExceedProbability()
						* rupture.getProbability();

				disaggMatrix[binIndex[0]][binIndex[1]][binIndex[2]][binIndex[3]][binIndex[4]] += annualRate;
				totalAnnualRate += annualRate;
			}  // end rupture loop
		}  // end source loop
		
		// TODO: normalize the matrix
		return disaggMatrix;

	}

	public boolean allInRange(
			double lat, double lon, double mag, double epsilon)
	{
		
		return inRange(this.latBinLims, lat)
				&& inRange(this.lonBinLims, lon)
				&& inRange(this.magBinLims, mag)
				&& inRange(this.epsilonBinLims, epsilon);
	}

	public static boolean inRange(Double[] bins, Double value)
	{
		return value >= bins[0] && value < bins[bins.length - 1];
	}

	/**
	 * Figure out which bins each input parameter fits into. The returned array
	 * of indices represent the 5 dimensional coordinates in the disaggregation
	 * matrix.
	 * @param lat
	 * @param lon
	 * @param mag
	 * @param epsilon
	 * @param trt
	 */
	public int[] getBinIndices(
			double lat, double lon, double mag,
			double epsilon, TectonicRegionType trt)
	{
		int[] result = new int[5];
		result[0] = digitize(this.latBinLims, lat);
		result[1] = digitize(this.lonBinLims, lon);
		result[2] = digitize(this.magBinLims, mag);
		result[3] = digitize(this.epsilonBinLims, epsilon);
		result[4] = Arrays.asList(TectonicRegionType.values()).indexOf(trt);

		return result;
	}

	public static int digitize(Double[] bins, Double value)
	{
		for (int i = 0; i < bins.length - 1; i++)
		{
			if (value >= bins[i] && value < bins[i + 1])
			{
				return i;
			}
		}
		throw new IllegalArgumentException(
				"Value '" + value + "' is outside the expected range");
	}

	/**
	 * Given a LocationList and a Location target, get the Location in the
	 * LocationList which is closest to the target Location.
	 * @param list
	 * @param target
	 * @return closest Location (in the input ListLocation) to the target
	 */
	public static Location closestLocation(LocationList list, Location target)
	{
		Location closest = null;

		double minDistance = Double.MAX_VALUE;

		for (Location loc : list)
		{
			double horzDist = LocationUtils.horzDistance(loc, target);
			double vertDist = LocationUtils.vertDistance(loc, target);
			double distance = Math.sqrt(Math.pow(horzDist, 2) + Math.pow(vertDist, 2));
			if (distance < minDistance)
			{
				minDistance = distance;
				closest = loc;
			}
		}
		return closest;
	}

	public static void normalize(double[][][][][] matrix, double normFactor)
	{
		for (int i = 0; i < matrix.length; i++)
		{
			for (int j = 0; j < matrix[i].length; j++)
			{
				for (int k = 0; k < matrix[i][j].length; k++)
				{
					for (int l = 0; l < matrix[i][j][k].length; l++)
					{
						for (int m = 0; m < matrix[i][j][k][l].length; m++)
						{
							matrix[i][j][k][l][m] /= normFactor;
						}
					}
				}
			}
		}
	}
}
