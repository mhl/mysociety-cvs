from sitestats.newsletters import common
from sitestats.newsletters.models import Newsletter
from sitestats.newsletters.formatting import render_table

class CommonBaseMeasuresNewsletter(Newsletter):
    
    class Meta:
        app_label = 'newsletters'
    
    site_id = None
    data = {}
    formats = {}
    sites = {}
    
    def template(self):
        return 'common_base_measures'
        
    def render(self, format, sources, date=None):
        """Returns the text for an email in text/html"""
        self.date=date
        if not self.formats.get(format):
            if not self.data:
                self.generate_data(sources, date)
            self.formats[format] =  self.render_data(format)
        return self.formats[format]
        
    def template_params(self, format):
        """Returns the text for a common base measures email in text/html"""
        week_start, week_end = self.week_bounds(self.date)
        summary_table = render_table(format, self.data['headers'], self.data['rows'], self.data['totals'])
        params = {'summary_table' : summary_table,
                  'week_start'    : week_start.strftime("%d/%m/%y"), 
                  'week_end'      : week_end.strftime("%d/%m/%y")}
        return params
    
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
                              ('% from search', 'percent_visits_from_search', '%', False),
                              ('% from sites', 'percent_visits_from_sites', '%', False),
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
            percent_change = common.percent_change(current, previous, unit)
            cell_info = {'current_value'  : current, 
                         'percent_change' : percent_change, 
                         'unit'           : unit}
            row.append(cell_info)
            if need_total:
                total = totals.get(header, 0)
                totals[header] = total + current_count
        return row

    def get_google_data(self, site_name, site_url, google, statistics, row, totals, date):
        this_week_end = date or common.end_of_current_week()
        previous_week_end = common.end_of_previous_week(this_week_end)
        for header, statistic, unit, need_total in statistics:
            method = getattr(google, statistic)
            current_data = method(site_name=site_name, site_url=site_url, date=this_week_end)
            previous_data = method(site_name=site_name, site_url=site_url, date=previous_week_end)
            current_count = current_data['resultcount']
            previous_count = previous_data['resultcount']
            percent_change = common.percent_change(current_count, previous_count, unit)
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
        self.get_google_data(site_info['name'], site_info['main_url'], sources['google'], stats['google'], row, totals, date)
        return row