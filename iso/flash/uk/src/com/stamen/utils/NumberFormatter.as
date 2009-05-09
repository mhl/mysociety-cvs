package com.stamen.utils
{
    public class NumberFormatter
    {
        public var decimalPlaces:uint;
        public var thousandsDelimiter:String = ',';
        public var decimalDelimiter:String = '.';

        public function NumberFormatter(decimalPlaces:uint=2)
        {
            this.decimalPlaces = decimalPlaces;
        }

        public function format(value:Number):String
        {
            var sign:String = (value >= 0) ? '' : '-';
            var out:String = value.toFixed(decimalPlaces);

            var exp:uint = Math.abs(value) >> 0;
            var man:uint = (decimalPlaces > 0) ? parseInt(out.split('.')[1]) : 0;
                        
            var expString:String = thousands(exp, thousandsDelimiter);

            if (decimalPlaces > 0)
            {
                var manString:String = zerofill(man, 2);
                return [sign, expString, decimalDelimiter, manString].join('');
            }
            else
            {
                return sign + expString;
            }
        }
        
        public static function thousands(value:int, separator:String=',', size:uint=3):String
        {
            var out:String = value.toString();
            var parts:Array = [];
            while (out.length > size)
            {
                var part:String = out.substr(-size);
                parts.unshift(part);
                out = out.substr(0, out.length - size);
            }
            parts.unshift(out);
            return parts.join(separator);
        }

        public static function zerofill(value:*, len:int=2):String
        {
            var out:String = String(value);
            while (out.length < len) out = '0' + out;
            return out;
        }
    }
}