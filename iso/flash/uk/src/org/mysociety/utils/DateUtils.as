package org.mysociety.utils
{
    public class DateUtils
    {
        public static function dateFromMinutesAfterMidnight(minutes:uint):Date
        {
            var d:Date = new Date();
            d.hours = d.minutes = d.seconds = 0;
            d.time += minutes * 60000;
            return d;
        }
    }
}