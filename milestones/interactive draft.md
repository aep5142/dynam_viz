# Financing Higher Education in Chile

Agustín Eyzaguirre

## Goal

It hasn't changed. It's about the difference in student State-backed loans in Chile for University students,
according to 4 main filters (region of Chile, year of loan granted, gender and income quintile).

Also, I will show the outcome of students once they finished/stopped studying. 

## Data Challenges

No, I'm relying on live data.

I had to clean and aggregate a 12 million row database for it.

## Walk Through

Once you run `index.html`, you'll face the map of Chile on the left and year,
income quintile and gender filters on the right.

When the program is ran, no filters are selected showing the totality of metrics that
have to be displayed.

There are two subsections: `CAE profile` and `Student Outcomes`.

In the first one there are two parts: the one in the top shows the "macro-data" 
delivering information on how many loans were granted using the filters chosen by the
user. The one in the bottom shows how does the "average student" looks like according
to the filters chosen by the user.

In `Student Outcomes`, after the user select filters, there will be a visualition
on how was the outcome of all student who finished or stopped studying. This part 
is still work in progress, yet the data is already live (if you go to console, the data
is being logged there).