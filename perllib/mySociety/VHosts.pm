package mySociety::VHosts;

use strict;
use warnings;

use Carp;
use File::Slurp;
use Path::Class qw(dir);

=head2 new

    $vhosts = mySociety::VHosts->new();
    $vhosts = mySociety::VHosts->new({ file => '/some/other/vhosts.pl' });

Returns a new vhosts object, by default created from '/data/servers/vhosts.pl'.
You can change this by specifying another file in $args.

=cut

sub new {
    my $class = shift;
    my $args = shift || {};

    my $self = {
        file => '/data/servers/vhosts.pl',
        %$args,
    };

    # sanity check
    croak "Can't find/read vhosts file '$self->{file}"    #
      unless -r $self->{file};

    # make an object.
    bless $self, $class;

    # load the sites, vhosts and databases
    $self->_load_entries_from_file();

    return $self;
}

sub _load_entries_from_file {
    my $self = shift;

    my $vhost_file     = $self->file;
    my $vhosts_content = read_file( $self->file )
      || croak "Could not read content from $vhost_file";

    # Eval the contents to set the variables
    my ( $sites, $vhosts, $databases );
    eval $vhosts_content;

    # check for any errors
    croak "Error evaling $vhost_file: $@" if $@;

    # store the results locally
    $self->{sites}     = $sites;
    $self->{vhosts}    = $vhosts;
    $self->{databases} = $databases;

    return $self;
}

=head2 file

    $file = $vhosts->file();

Return the file that the vhosts were read from.

=cut

sub file {
    return $_[0]->{file};
}

=head2 site, vhost, database

    $site_config     = $vhosts->site('fixmystreet');
    $vhost_config    = $vhosts->vhost('www.fixmystreet.com');
    $database_config = $vhosts->database('bci');

Return the config hashref from vhosts.pl for the requested entry. If the entry
is not found it croaks.

=cut

sub site     { return $_[0]->_entry( sites     => $_[1] ); }
sub vhost    { return $_[0]->_entry( vhosts    => $_[1] ); }
sub database { return $_[0]->_entry( databases => $_[1] ); }

sub _entry {
    my ( $self, $key, $name ) = @_;

    my $entry = $self->{$key}{$name}
      || croak "Can't find an entry in '$key' for '$name'";

    return $entry;
}

=head2 all_vhosts_backup_dirs

    $entry_list = $vhosts->all_vhosts_backup_dirs();
    $entry_list = $vhosts->all_vhosts_backup_dirs( { make_dirs_absolute => 1 } );

Returns all the directories that need to be backed up as an arrayref of entries.
Setting make_dirs_absolute to true will return the list with all paths made
absolute.

    $entry_list = [
        {
            vhost   => 'www.mysociety.org',
            servers => ['arrow'],
            dir     => '/absolute/path/to/dir',
        },
        {
            vhost   => 'www.mysociety.org',
            servers => ['arrow'],
            dir     => 'relative/path',
        },
        ...
    ];

=cut

sub all_vhosts_backup_dirs {
    my $self    = shift;
    my $args    = shift || {};
    my @entries = ();

    # flags
    my $make_dirs_absolute = $args->{make_dirs_absolute} || 0;

    foreach my $vhost_name ( sort keys %{ $self->{vhosts} } ) {

        my $vhost      = $self->vhost($vhost_name);
        my $vhost_base = "/data/vhost/$vhost_name/mysociety";

        foreach my $dir ( @{ $vhost->{backup_dirs} || [] } ) {

            # TODO - add '->resolve' below once the Path::Class
            # shipped by debian is less ancient

            if ( $make_dirs_absolute && !dir($dir)->is_absolute ) {
                $dir = dir($dir)             #
                  ->absolute($vhost_base)    # absolute based on vhost dir
                                             # ->resolve() # collapse '/foo/../'
                  ->stringify;               # make it a string
            }

            push @entries,
              {
                vhost   => $vhost_name,
                servers => $vhost->{servers},
                dir     => $dir,
              };
        }
    }

    return \@entries;
}

1;
