-- ================================================
-- HOTEL REVENUE MANAGEMENT - SQL ANALYSIS
-- Author: [Your Name]
-- Date: January 2026
-- Database: hotel_revenue
-- ================================================

USE hotel_revenue;

-- ================================================
-- ANALYSIS 1: Revenue by Market Segment
-- Purpose: Identify which channel generates most revenue
-- Business Question: "Where should we invest marketing budget?"
-- ================================================

SELECT
    market_segment_type AS segment
    COUNT(Booking_ID) AS total_bookings,
    SUM(CASE WHEN booking_status = 'Not_Canceled' THEN 1 ELSE 0 END) AS confirmed_bookings,
    (COUNT(Booking_ID) - SUM(CASE WHEN booking_status == 'Not_Canceled' THEN 1 ELSE 0 END)) AS canceled_bookings,
    ROUND(AVG(avg_price_per_room), 2) AS adr,
    ROUND(SUM(CASE WHEN booking_status = 'Not_Canceled' THEN total_revenue ELSE 0 END), 2) AS total_revenue
    ROUND(AVG(CASE WHEN booking_status = 'Not_Canceled' THEN total_nights ELSE NULL END), 1) AS avg_nights
FROM reservations
GROUP BY market_segment_type
ORDER BY total_revenue DESC;

-- ================================================
-- ANALYSIS 2: Monthly Revenue Trend
-- Purpose: Identify seasonality patterns
-- Business Question: "When should we increase prices? When to promote?"
-- ================================================

SELECT
    arrival_year AS year,
    arrival_month AS month,
    COUNT(Booking_ID) AS total_bookings,
    SUM(CASE WHEN booking_status = 'Not_Canceled' THEN 1 ELSE 0 END) AS confirmed_bookings,
    ROUND(AVG(avg_price_per_room), 2) AS adr,
    ROUND(SUM(CASE WHEN booking_status = 'Not_Canceled' THEN total_revenue ELSE 0 END), 2) AS total_revenue,
    ROUND(
        (SUM(CASE WHEN booking_status = 'Canceled' THEN 1 ELSE 0 END) / COUNT(Booking_ID)) * 100,
        1
    ) AS cancellation_rate_pct
FROM reservations
GROUP BY arrival_year, arrival_month
ORDER BY arrival_year, arrival_month;

-- ================================================
-- ANALYSIS 3: Cancellation Analysis
-- Purpose: Understand WHY cancellation rate is so high (45%+)
-- Business Question: "What factors influence cancellations?"
-- ================================================

SELECT
    -- Categorize lead time into buckets
    CASE
        WHEN lead_time < 7 THEN '1. Last Minute (0-6 days)'
        WHEN lead_time < 30 THEN '2. Short Notice (7-29 days)'
        WHEN lead_time < 90 THEN '3. Standard (30-89 days)'
        WHEN lead_time < 180 THEN '4. Early Booking (90-179 days)'
        ELSE '5. Very Early (180+ days)'
    END AS booking_window,
    COUNT(Booking_ID) AS total_bookings,
    SUM(CASE WHEN booking_status = 'Canceled' THEN 1 ELSE 0 END) AS canceled_bookings,
    ROUND(
        (SUM(CASE WHEN booking_status = 'Canceled' THEN 1 ELSE 0 END) / COUNT(Booking_ID)) * 100,
        1
    ) AS cancellation_rate_pct,
    ROUND(AVG(lead_time), 0) AS avg_lead_time_days,
    ROUND(AVG(CASE WHEN booking_status = 'Not_Canceled' THEN avg_price_per_room ELSE NULL END)) AS adr
FROM reservations
GROUP BY booking_window
ORDER BY booking_window;

-- ================================================
-- ANALYSIS 4: Room Type Performance
-- Purpose: Identify most profitable room types
-- Business Question: "Which rooms should we invest in? Which to phase out?"
-- ================================================

SELECT
    room_type_reserved AS room_type,
    COUNT(Booking_ID) AS total_bookings,
    SUM(CASE WHEN booking_status = 'Not_Canceled' THEN 1 ELSE 0 END) AS confirmed_bookings,
    ROUND(
        (SUM(CASE WHEN booking_status = 'Canceled' THEN 1 ELSE 0 END) / COUNT(Booking_ID)) * 100,
        1) AS cancellation_rate_pct,
    ROUND(AVG(CASE WHEN booking_status = 'Not_Canceled' THEN avg_price_per_room ELSE NULL END), 2) AS adr, 
    ROUND(SUM(CASE WHEN booking_status = 'Not_Canceled' THEN total_revenue THEN 0 END), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN booking_status = 'Not_Canceled' THEN total_nights ELSE NULL END), 2) AS total_nights,
    ROUND(AVG(CASE WHEN booking_status = 'Not_Canceled' THEN total_guest ELSE NULL END), 2) AS total_guest,
    -- Revenue efficiency metric
    ROUND(
        SUM(CASE WHEN booking_status = 'Not_Canceled' = total_revenue ELSE 0 END) /
        SUM(CASE WHEN booking_status = 'Not_Canceled' = 1 ELSE 0 END),
        2) AS revenue_per_confirmed_booking
FROM reservations
GROUP BY room_type_reserved
ORDER BY total_revenue DESC;
