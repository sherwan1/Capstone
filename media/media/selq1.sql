SET SEARCH_PATH TO parlgov;
drop table if exists q1 cascade;

SELECT pres.id as president,party.name as party
                                FROM politician_president pres,party,country
                                WHERE pres.country_id = country.id AND
                                pres.party_id = party.id AND
                                country.name = 'France'
                                ORDER BY pres.end_date DESC;