/* mySociety customised version of Stamen's Flash application */

package
{
    import UKTransitTime;
    import org.mysociety.map.providers.ColCloudMadeProvider;

    public class ColUKTransitTime extends UKTransitTime
    {
        public function ColUKTransitTime()
        {
            super();

            // Use URL for our own proxy of CloudMade.
            // Also fixes bug in pattern that tiles are loaded from different
            // servers with.
            map.displayMap.setMapProvider(new ColCloudMadeProvider())
        }
    }
}

