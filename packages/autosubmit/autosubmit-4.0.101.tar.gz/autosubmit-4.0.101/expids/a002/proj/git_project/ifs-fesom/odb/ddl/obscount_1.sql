//
// obscount_1.sql 
//
// Created:   16-Oct-2007  : Sami Saarinen, ECMWF (SS)
// Modified:  19-Oct-2007  : sum(index.len) -> sum(hdr.len) & ORDERBY adjusted
//

READONLY;

CREATE VIEW obscount_1 AS
SELECT timeslot@timeslot_index,sum(hdr.len),sum(body.len) 
  FROM timeslot_index,index,hdr 
ORDERBY -2,-3,1;

