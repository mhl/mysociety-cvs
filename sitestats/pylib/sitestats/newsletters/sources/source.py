class Source:
        
    def get_top_n(self, data, limit=None, keep_values=False):
        """Takes a hash of numeric values keyed by strings and returns a list of the top n (defaulting to all if no
        limit is supplied), sorted by value"""
        data = [ (value, key) for key, value in data.items()]
        data.sort()
        data.reverse()
        if limit:
            data = data[:limit]
        if keep_values:
            data = [ (key, value) for (value, key) in data ]
        else:
            data = [ key for (value, key) in data ]
        return data
    