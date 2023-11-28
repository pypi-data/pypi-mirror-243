//
//-- ODB/SQL file 'matchup_procid.sql'
//
//   Last updated:  28-Jan-2005
//

CREATE VIEW matchup_procid AS
  SELECT procid
    FROM index
   WHERE #index == 1  // The first row is sufficient
;
