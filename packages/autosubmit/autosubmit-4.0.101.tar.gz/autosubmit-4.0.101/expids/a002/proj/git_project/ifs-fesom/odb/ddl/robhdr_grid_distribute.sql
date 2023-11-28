//
//-- ODB/SQL file 'robhdr_grid_distribute.sql'
//
//   Created:  22-Jun-2009
//


READONLY; // .. except where  UPDATED qualifier was found

CREATE VIEW robhdr_grid_distribute AS
  SELECT seqno,                         // MDBONM (must be the first index; used to build MLNKH2B)
         lat,                           // MDBLAT
         lon,                           // MDBLON
         distribid UPDATED,             // mdb_distribid_at_hdr
         gp_dist UPDATED,               // MDB_GP_DIST hdr
         gp_number UPDATED,             // MDB_GP_NUMBER hdr
         distribtype,
  FROM   hdr
  WHERE  distribtype IS NOT NULL AND distribtype > 0 // only observations on the model grid
;

