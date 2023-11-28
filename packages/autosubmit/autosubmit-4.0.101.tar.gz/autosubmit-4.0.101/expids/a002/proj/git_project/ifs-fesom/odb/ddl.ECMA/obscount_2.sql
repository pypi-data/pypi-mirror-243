//
// obscount_2.sql 
//
// Created:   02-Nov-2007  : Sami Saarinen, ECMWF
//

READONLY;

CREATE VIEW obscount_2 AS
SELECT timeslot,sum(index.len)
  FROM timeslot_index
ORDERBY -2, 1

