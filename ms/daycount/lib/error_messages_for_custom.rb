module ActionView
    module Helpers
        module ActiveRecordHelper    
           def error_messages_for_custom(object_name, options = {})
             options = options.symbolize_keys    
             object = instance_variable_get("@#{object_name}")
             unless object.errors.empty?
               content_tag("div",
                 content_tag(
                   options[:header_tag] || "b",
                   "#{pluralize(object.errors.count, "error")} prevented this #{object_name.to_s.gsub("_", " ")} from being saved"
                 ) +
                 content_tag("p", "There were the following problems:") +
                 content_tag("ul", object.errors.full_messages.collect { |msg| content_tag("li", msg) }),
                 "id" => options[:id] || "errorExplanation", "class" => options[:class] || "errorExplanation"
              )
            end
          end
       end
    end
end