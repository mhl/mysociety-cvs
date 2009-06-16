from django.db import models
from django.contrib.auth.models import User
from sitestats.newsletters import common
from formatting import render_table, format_cell_value
from django.db.models import signals
from django.core.exceptions import ObjectDoesNotExist

class Newsletter(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
    
    def render(self, format, sources, date=None):
        return "Abstract"
        
class CommonBaseMeasuresNewsletter(Newsletter):
    
    data = {}
    formats = {}
    
    def render(self, format, sources, date=None):
        """Returns the text for a common base measures email in text/html"""
        if not self.formats.get(format):
            if not self.data:
                self.generate_data(sources, date)
            rendered = render_table(format, self.data['headers'], self.data['rows'], self.data['totals'])
            self.formats[format] = rendered
        return self.formats[format]
    
    def generate_data(self, sources, date):
        sites = sources['piwik'].sites()
        stats = self.stats()
        rows = []
        stat_totals = {}
        for site_info in sites: 
            row = [site_info['name']]
            row += self.get_data(site_info, sources, stat_totals, date)
            rows.append(row)

        headers = ['site']
        totals = []
        for (header, stat, unit, need_total) in stats['piwik'] + stats['google']:
            headers.append(header)
            total_val = stat_totals.get(header)
            if need_total:
                totals.append(total_val)
            else:
                totals.append('')
        self.data['headers'] = headers
        self.data['rows'] = rows
        self.data['totals'] = totals
        
    def stats(self):
        """Returns a dictionary keyed by data source whose values are lists of tuples. Each tuple consists of the name of a
        statistic to be gathered, the method on the source class to use to get it, the units string to be used in displaying it, 
        and whether a total should be generated for this statistic."""
        
        stats =  {'piwik'  : [('unique visitors', 'unique_visitors', '', False), 
                              ('visits', 'visits', '', False),
                              ('bounce rate', 'bounce_rate', '%', False), 
                              ('% from search', 'percent_visitors_from_search', '%', False),
                              ('% from sites', 'percent_visitors_from_sites', '%', False),
                              ('page views/visit', 'pageviews_per_visit', '', False),
                              ('time/visit', 'time_per_visit', 's', False)], 
                  'google' : [('news articles', 'news', '', True), 
                              ('blog posts', 'blogs', '', True)]}
        return stats

    def get_piwik_data(self, site_id, piwik, statistics, row, totals, date):
        """Gets the data for base measures for a site from piwik"""
        this_week_end = date or common.end_of_current_week()
        previous_week_end = common.end_of_previous_week(this_week_end)
        for header, statistic, unit, need_total in statistics:
            method = getattr(piwik, statistic)
            current = method(site_id=site_id, date=this_week_end)
            previous = method(site_id=site_id, date=previous_week_end)
            percent_change = common.percent_change(current, previous)
            cell_info = {'current_value'  : current, 
                         'percent_change' : percent_change, 
                         'unit'           : unit}
            row.append(cell_info)
            if need_total:
                total = totals.get(header, 0)
                totals[header] = total + current_count
        return row

    def get_google_data(self, site_name, google, statistics, row, totals, date):
        this_week_end = date or common.end_of_current_week()
        previous_week_end = common.end_of_previous_week(this_week_end)
        for header, statistic, unit, need_total in statistics:
            method = getattr(google, statistic)
            current_data = method(site_name=site_name, date=this_week_end)
            previous_data = method(site_name=site_name, date=previous_week_end)
            current_count = current_data['results']
            previous_count = previous_data['results']
            percent_change = common.percent_change(current_count, previous_count)
            cell_info = {'current_value'  : current_count, 
                         'percent_change' : percent_change, 
                         'unit'           : unit, 
                         'link'           : current_data['url']}
            row.append(cell_info)
            if need_total:
                total = totals.get(header, 0)
                totals[header] = total + current_count
        return row

    def get_data(self, site_info, sources, totals, date=None):
        stats = self.stats()
        row = []
        self.get_piwik_data(site_info['id'], sources['piwik'], stats['piwik'], row, totals, date)
        self.get_google_data(site_info['name'], sources['google'], stats['google'], row, totals, date)
        return row        

class Subscription(models.Model):
    """Subscriptions of users to newsletters"""
    newsletter = models.ForeignKey(Newsletter)
    user = models.ForeignKey(User)
    
class Profile(models.Model):
    """User profile model"""
    FORMAT_CHOICES = ((0, 'html'), 
                      (1, 'text'))
                       
    user = models.OneToOneField(User, primary_key=True)
    one_email = models.BooleanField(default=False)
    email_format = models.IntegerField(choices=FORMAT_CHOICES, default=0)

def add_user_profile(sender, **kwargs):
    """Create a user profile for any user that is saved and doesn't already have one"""
    instance = kwargs['instance']
    try:
        instance.profile
    except ObjectDoesNotExist:
        profile = Profile(user=instance)
        profile.save()

signals.post_save.connect(add_user_profile, sender=User)
