//
// Created by Anne Fouilloux - 13/04/2010
//
CREATE VIEW time_info AS
SELECT distinct timeslot, enddate, endtime
FROM   timeslot_index
ORDERBY timeslot
;
