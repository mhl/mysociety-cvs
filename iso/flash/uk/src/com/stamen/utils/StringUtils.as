package com.stamen.utils
{
    public class StringUtils
    {
        public static var stopWords:Array = ['of', 'from', 'and', 'in', 'with', 'w/'];
        
        public static function pluralize(value:Number, singular:String, plural:String=null):String
        {
            return (value == 1)
                   ? singular
                   : plural || singular + 's';
        }
        
        public static function capitalize(str:String, ...rest):String
        {
            var out:String = str.toLowerCase();
            if (stopWords.indexOf(out) >= 0) return out;
            return out.substr(0, 1).toUpperCase() + out.substr(1);
        }
        
        public static function capitalizeWords(str:String):String
        {
            var parts:Array = str.split(/ +/);
            return parts.map(capitalize).join(' ');
        }
        
        public static function replace(str:String, replacements:Object):String
        {
            if (!replacements) return str;
            
            var out:String = str;
            if (replacements is Array)
            {
                for (var i:int = 0; i < replacements.length; i += 2)
                {
                    out = out.replace(replacements[i], replacements[i + 1]);
                }
            }
            else
            {
                for (var find:String in replacements)
                {
                    if (!find) continue;
                    out = out.replace(find, String(replacements[find]));
                }
            }
            return out;
        }
    }
}