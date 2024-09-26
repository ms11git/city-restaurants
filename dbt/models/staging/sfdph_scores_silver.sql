SELECT UPPER(business_name) as business_name
, address
, UPPER(purpose) as purpose
, PARSE_DATE('%B %d, %Y', inspection_date) as inspection_date
, UPPER(facility_rating_status) as facility_rating_status
FROM `external_data`.`sfdph_scores_bronze`
GROUP BY 1,2,3,4,5