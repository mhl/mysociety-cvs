#!/usr/bin/perl

package Amazon::QueryAccessXinoXPath;

use strict;

use HTTP::Request;
use HTTP::Response;
use LWP::Simple;
use Time::HiRes;
use XML::XPath;
use LWP::UserAgent;


##
## CONSTRUCTOR
##
sub new {
  my ($class) = @_;
  
  my $self = bless {
		   }, $class;
  
  return $self;
}

##
## 'PUBLIC' METHODS
##


sub make_query {
  # accept: country, test/live, API version, & AWS xml/http call
  # return: webserver response time, http code, request type (unused?) & XML reply from AWS
  my ($self, $url, $query_string) = @_;

# CHANGED FOR 4.0 - hard code REST path
  my $full_url = "$url";

  # now compile the full URL
  my $url_string = $full_url . $query_string;
  

  # push query, grab result
  my $browser = new LWP::UserAgent;
  my $request = new HTTP::Request('POST', $url_string);
  my ($raw_response, $xpath_response);
  my ($t0, $t1);
  eval {
    $t0 = Time::HiRes::gettimeofday * 1000;
    $raw_response = $browser->request($request);
    $t1 = Time::HiRes::gettimeofday * 1000;
  };

  # grab the method 
  my $method;
  if ($query_string =~ /Action=(.*?)\&/) {
    $method = $1;
  }
  
  my $elapsed_msecs = $t1 - $t0;
  my $response_code = $raw_response->status_line();

  if ($raw_response) {
    eval {
      $xpath_response = XML::XPath->new(xml => $raw_response->content());
    }
  } else {
    print "No response for this test\n";
  }

  # package data for return
  return $xpath_response;

}

1;
