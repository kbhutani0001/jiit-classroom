# JIIT Classroom

## Platform to take online classes and exams for JIIT - 128 students
## Used by 15+ professors and 500+ students for online classes 

## Problem Statement:
During COVID-19 pandemic, teachers had to shift all classes to online platforms like Zoom, Cisco webx. But the main problem they were facing is **Class Bombing**. Many students/unknown people will join meeting with random names and start disturbing the whole class. Many cases started coming, some even showed inappropriate content by sharing there screens. It was impossible for teachers to conduct classes. Another problem was faced when taking the attendance. In a 40 minute meeting, 10 minutes were wasted taking attendance and some students will join the meeting at the end just for the sake of it.

## Solution
During end of march, I came up with an idea to add an extra layer of security before the meetings. I thought of using College's own login system (webkiosk) to authenticate students as anyone can create a fake zomm,cisco,google ID but no one can create a fake college ID. So basically, JIIT Classroom asks students to Log in through webkiosk before joining the meeting. If they enter right combination of Login ID and password, the details are fetched automatically from the Webkiosk's server and the meeting name is automatically set to their **EnrollmentNumber_Name** which cannot be changed. So this allowed full transperancy, teachers were able to see who joined the meeting, who is speaking and on the top of it, the attendance is also recorded automatically along with Joining time of students.


