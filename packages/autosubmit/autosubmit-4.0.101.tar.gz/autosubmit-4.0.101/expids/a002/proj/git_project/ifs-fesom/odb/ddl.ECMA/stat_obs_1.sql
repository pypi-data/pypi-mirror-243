//
// Created by Anne Fouilloux - 13/04/2010
//
CREATE VIEW stat_obs_1 AS
SELECT obstype,codetype
FROM hdr 
ORDERBY obstype, codetype
;
