//
//-- ODB/SQL file 'caifc1.sql'
//
//   Last updated:  14-Nov-2018
//

READONLY;

CREATE VIEW caifc1 AS
  SELECT fg_depar,
         hires UPDATED
    FROM body, update[1]
;
