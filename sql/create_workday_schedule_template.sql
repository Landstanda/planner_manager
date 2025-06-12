-- Create a complete 24-hour workday schedule template
-- Clear existing data first (optional)
DELETE FROM schedule_template WHERE day_type = 'workday';

-- Complete 24-hour workday schedule
INSERT INTO schedule_template (day_type, start_time, end_time, block_type, description, priority_for_type) VALUES
-- Sleep: 10:00 PM - 7:00 AM (9 hours)
('workday', '22:00:00', '07:00:00', 'personal', 'Sleep', 1),

-- Morning Routine: 7:00 AM - 8:00 AM (1 hour)
('workday', '07:00:00', '08:00:00', 'personal', 'Morning Routine', 2),

-- Work Block 1: 8:00 AM - 10:00 AM (2 hours)
('workday', '08:00:00', '10:00:00', 'work', 'Work Block 1', 3),

-- Breakfast: 10:00 AM - 10:30 AM (30 minutes)
('workday', '10:00:00', '10:30:00', 'personal', 'Breakfast', 2),

-- Work Block 2: 10:30 AM - 12:15 PM (1 hour 45 minutes)
('workday', '10:30:00', '12:15:00', 'work', 'Work Block 2', 3),

-- Break: 12:15 PM - 1:00 PM (45 minutes)
('workday', '12:15:00', '13:00:00', 'personal', 'Lunch Break', 2),

-- Work Block 3: 1:00 PM - 3:00 PM (2 hours)
('workday', '13:00:00', '15:00:00', 'work', 'Work Block 3', 3),

-- Family Time 1: 3:00 PM - 4:00 PM (1 hour)
('workday', '15:00:00', '16:00:00', 'personal', 'Family Time', 2),

-- Work Block 4: 4:00 PM - 6:00 PM (2 hours)
('workday', '16:00:00', '18:00:00', 'work', 'Work Block 4', 3),

-- Family Play Time: 6:00 PM - 7:30 PM (1.5 hours)
('workday', '18:00:00', '19:30:00', 'personal', 'Family Play Time', 2),

-- Relaxing: 7:30 PM - 10:00 PM (2.5 hours)
('workday', '19:30:00', '22:00:00', 'personal', 'Relaxing Before Bed', 1); 