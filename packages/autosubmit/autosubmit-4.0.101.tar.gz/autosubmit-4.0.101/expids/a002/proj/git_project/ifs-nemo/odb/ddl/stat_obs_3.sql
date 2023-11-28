//
// Created by Anne Fouilloux - 13/05/2012
//

READONLY;

CREATE VIEW stat_obs_3 AS
SELECT count(obsvalue), varno, reportype
FROM hdr, body where fg_depar IS NOT NULL
;
