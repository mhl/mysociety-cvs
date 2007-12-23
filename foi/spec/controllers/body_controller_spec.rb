require File.dirname(__FILE__) + '/../spec_helper'

describe BodyController, "when showing a body" do
    integrate_views
    fixtures :public_bodies, :public_body_versions
  
    it "should be successful" do
        get :show, :simple_short_name => "dfh"
        response.should be_success
    end

    it "should render with 'show' template" do
        get :show, :simple_short_name => "dfh"
        response.should render_template('show')
    end

    it "should assign the body" do
        get :show, :simple_short_name => "dfh"
        assigns[:public_bodies].should == [ public_bodies(:humpadink_public_body) ]
    end

    it "should redirect to newest name if you use historic name of public body in URL" do
        get :show, :simple_short_name => "hdink"
        response.should redirect_to(:controller => 'body', :action => 'show', :simple_short_name => "dfh")
    end
    
    # XXX test for 404s when don't give valid name
    # XXX test the fancy history searching stuff
end
