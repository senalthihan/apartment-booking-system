# Apartment Booking System

A Python command-line application for managing apartment bookings, 
supplementary items, reward points, and order history for a 
short-stay accommodation business.

## Tools & Concepts
Python, OOP (Inheritance, Encapsulation, Exception Handling), 
CSV File I/O

## Features
- **Guest Management** — Add guests, track reward points balance, 
  set custom reward and redeem rates
- **Product Catalogue** — Manage apartment units, supplementary 
  items (breakfast, car park), and product bundles
- **Multi-Item Orders** — Book apartments with check-in/check-out 
  dates, add supplementary items, apply reward point discounts
- **Receipt Generation** — Prints itemised receipt with subtotals, 
  discounts, and earned points
- **Order History** — View full booking history per guest
- **Statistics Export** — Generates top 3 guests by spend and 
  top 3 products by quantity sold, saved to stats.txt
- **CSV Persistence** — Load and save guests, products, and 
  orders across sessions

## How to Run
```bash
python ProgFunA2_s4099547.py -g guests.csv -p products.csv 
-o orders.csv
```
