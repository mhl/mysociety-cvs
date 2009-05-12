package org.mysociety.utils
{
    import com.stamen.utils.StringUtils;
    
    public class DateUtils
    {
        public static function dateFromMinutesAfterMidnight(minutes:uint):Date
        {
            var d:Date = new Date();
            d.hours = d.minutes = d.seconds = 0;
            d.time += minutes * 60000;
            return d;
        }
        
        public static function relativeTimeString(minutes:uint, minuteString:String='minute', hourString:String='hour'):String
        {
            trace('* got', minutes, 'minutes');
            if (minutes > 60)
            {
                var hours:uint = minutes / 60;  
                var out:String = hours + ' ' + StringUtils.pluralize(hours, hourString);
                minutes %= 60;
                if (minutes > 0)
                {
                    return out + ', ' + minutes + ' ' + StringUtils.pluralize(minutes, minuteString);
                }
                return out;
            }
            return minutes + ' ' + StringUtils.pluralize(minutes, minuteString);
        }
    }
}