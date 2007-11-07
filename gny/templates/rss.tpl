<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:georss="http://www.georss.org/georss">
	<channel>
		<title>{$site_name} - groups near {$query_display_text|escape:html}</title>
		<link>{$search_link}</link>
		<description>{$site_tag_line}</description>
        {foreach name="groups" from="$groups" item="group"}
            <item>
                <title>New group! {$group->name|escape:html} - {$group->byline|escape:html}</title>
                <pubDate>{$group->created_date|date_format:"%a, %e %b %Y"}</pubDate>                
                <guid isPermaLink="true">{$www_server}/groups/{$group->url_id}</guid>
                <georss:featurename>{$group->name|escape:html}</georss:featurename>
                <georss:box>{$group->lat_bottom_left} {$group->long_bottom_left} {$group->lat_top_right} {$group->long_top_right}</georss:box>
                <description><![CDATA[{$group->description|escape:html}]]></description>
                <link><![CDATA[{$www_server}/groups/{$group->url_id}/]]></link>
            </item>
        {/foreach}
    </channel>
</rss>
