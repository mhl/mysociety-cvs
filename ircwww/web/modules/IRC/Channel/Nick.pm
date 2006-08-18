# $Id: Nick.pm,v 1.1 2006-08-18 12:15:26 francis Exp $
package IRC::Channel::Nick;
use strict;

sub new {
   my $class = shift;
   my $self = bless { }, $class;
   %$self = @_;
   return $self;
}

# Maybe i'll add some functions here, one day...

1;
