{textformat style='email'}

GROUPS ADDED IN THE PAST {$days} DAYS:

{foreach from=$groups item=group}

{$group->name} [{$www_server}/groups/{$group->url_id}]
{/foreach}


--------


ALL TIME STATS:

{foreach from=$stats item=stat}

    {$stat->stat_key}:  {$stat->value}
    
    
{/foreach}


--------


You are recieveing these emails because you are on the {$team_email} mailing list
{/textformat}