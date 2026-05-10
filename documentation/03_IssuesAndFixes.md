# 🐞 Issues Found and Fixes

## 3.1 Background Image Not Displaying

The background image did not load due to:

- Incorrect folder path
- Wrong file name
- Browser caching

**Fix:**  
I corrected the path, verified the file name, and refreshed the browser cache.

---

## 3.2 Missing Time Units

Initially, the script only displayed hours.  
I expanded the time breakdown to include:

- Years
- Days
- Hours
- Minutes
- Seconds

Later, I removed milliseconds to keep the display clean and cinematic.

---

## 3.3 Incorrect Miller Time Conversion

The first version did not apply the correct time‑dilation formula.

I fixed it using:

1 hour on Miller = 7 years on Earth

Converted to milliseconds:

7 _ 365 _ 24 _ 60 _ 60 \* 1000

Then I recalculated Miller time properly.

---

## 3.4 Missing Start and Current Date

I added:

- A fixed start date: **November 7, 2014 at 00:00**
- A dynamic current date
- Automatic updates every second

---

## 3.5 Text Visibility Problems

The text was hard to read over the Gargantua background.

**Fix:**  
I added:

- Animated color shifting
- Black text stroke
- Soft shadow

---

## 3.6 Missing Informational Text

I added a dynamic explanation:

> “Time has been running since November 7, 2014 at 00:00, based on the rule that 1 hour on Miller equals 7 years on Earth.”

---

## 3.7 Visit Counter Not Implemented

I integrated **CountAPI**, a free service that tracks visits.

Every time someone loads the page:

- CountAPI increments the counter
- The script fetches the updated value
- The page displays it under “Visits”
