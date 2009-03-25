//
// performance_monitor.cpp:
// Outputs timings round sections of code.
//
// Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org; WWW: http://www.mysociety.org/
//
// $Id: performance_monitor.h,v 1.2 2009-03-25 12:06:29 francis Exp $
//

/* Measures wall clock use 
 * XXX wanted crude memory measure here, but couldn't find an easy one to use */
class PerformanceMonitor {
    std::string name;
    clock_t clock_before;
    FILE *out;

    public:

    PerformanceMonitor(FILE *l_out = stderr) : out(l_out) {
        reset();
    }
    
    void reset() {
        this->clock_before = clock();
    }

    void display(const std::string& desc) {
        fprintf(this->out, "%s: ", desc.c_str());

        clock_t clock_after = clock();
        fprintf(this->out, "%f secs ", double(clock_after - this->clock_before) / double(CLOCKS_PER_SEC));
        
        fprintf(this->out, "\n");

        this->reset();
    }

};


