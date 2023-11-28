//
//-- ODB/SQL file 'getrsondeid.sql'
//
//   Last updated:  08-Oct-2012
//

READONLY;

CREATE VIEW getrsondeid AS
     SELECT DISTINCT reportype,statid,sonde_type
      FROM hdr, body, conv
      WHERE obstype = $temp and varno@body = $t
;

// Notes:
// 1. if the elements in the SELE.CT are changed, remember to update varbc_rsonde.F90
// 2. if the list of varno in the WHE.RE are changed, remember to update
//        hdepart.F90, hretr.F90, hop.F90, hoptl.F90, and hopad.F90

