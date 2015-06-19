# udacity-p4

## Using API explorer
**App-id** = "conference-organization"  
**API explorer** = https://apis-explorer.appspot.com/apis-explorer/?base=https://conference-organization.appspot.com/_ah/api#p/conference/v1/  

## Task 1: Add Sessions to a Conference
Speaker was implemented as a simple `String`. Main reason for that was simplicity, although in real-world project that would have to be transformed to separate Kind.  
Currently, it has several flaws. First of all, there's data duplication. In addition, we probably will have to add some additional info about speakers (like an email address).  

Session has different time format than `SessionForm`, which consists of `startTime` ("13:00"), `duration` (90 [minutes]), `date` ("2016-01-05") .   
Session converts those fields into two `DateTime` properties - `startDate` and `endDate`.  
In order to make queries against `duration` (while looking for longest session) and `startHour` (Task 3) it uses two `ComputedProperties`, which calculates those value based on start and end dates. 

## Task 3: Work on indexes and queries
### Additional queries
`getLongestSessions(websafeConferenceKey)`  
Returns longest session for given conference.  

`getMostActiveSpeaker()`  
Returns speaker, who has given most sessions across all conferences so far.  

### "you don't like workshops and you don't like sessions before 7 pm" query problem  
This query requires inequality filters for two properties (`type != workshop AND startHour > 19`), which isn't supported by GAE.  
Solution is provided in `getNotWorkshopsSessionsAfter7PM()`.  
Basically, it keeps `startHour > 19` filter and changes `type != workshop` filter to `type IN desired_session_types`,  
where `desired_session_types` is array of all session types found in DB (except 'workshop'). 