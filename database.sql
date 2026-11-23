-- ============================================================
-- Plant Stress Detective - Database Schema
-- Class 12 Computer Science Project (Python + MySQL)
-- ============================================================

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS plant_stress_db;
USE plant_stress_db;

-- 2. Create the Table for Plant Observations
CREATE TABLE IF NOT EXISTS plant_observations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plant_name VARCHAR(100) NOT NULL,
    moisture_pct FLOAT NOT NULL,
    temperature_c FLOAT NOT NULL,
    leaf_condition VARCHAR(50) NOT NULL,
    stress_level VARCHAR(50) NOT NULL,
    stress_indicators TEXT NOT NULL,
    care_suggestions TEXT NOT NULL,
    notes VARCHAR(255) DEFAULT '',
    observed_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Insert Sample Data for Demonstration
INSERT INTO plant_observations 
(plant_name, moisture_pct, temperature_c, leaf_condition, stress_level, stress_indicators, care_suggestions, notes)
VALUES
('Tomato', 22.0, 32.0, 'Yellow', 'Moderate Stress', 
 'Under-watering indicator: soil moisture (22.0%) is below threshold (30%). Leaf chlorosis: yellow leaves reported.', 
 '1. Water the plant thoroughly at the base. 2. Inspect sunlight exposure and check soil nitrogen levels. 3. Monitor leaf recovery over 48 hours.', 
 'Balcony container garden'),

('Money Plant', 78.0, 24.0, 'Yellow', 'Moderate Stress', 
 'Over-watering indicator: soil moisture (78.0%) exceeds 70%. Risk of root suffocation.', 
 '1. Pause watering immediately. 2. Ensure container drainage holes are clear. 3. Allow upper 2 inches of soil to dry before watering again.', 
 'Indoor living room pot'),

('Snake Plant', 45.0, 23.0, 'Healthy', 'Optimal Condition', 
 'Moisture and temperature are in optimal range. Leaves appear firm and healthy.', 
 '1. Maintain current balanced care schedule. 2. Continue bright indirect lighting.', 
 'Study desk planter'),

('Rose', 18.0, 36.0, 'Dry / Crispy', 'Severe Stress', 
 'Severe drought and heat stress: low moisture (18.0%) and high temperature (36.0°C). Brittle leaf tissue.', 
 '1. Provide immediate deep watering. 2. Move to partial shade or erect a temporary shade cloth. 3. Apply organic mulch to retain soil moisture.', 
 'Terrace flowerbed'),

('Basil', 35.0, 11.0, 'Wilting', 'Moderate Stress', 
 'Cold shock stress: ambient temperature (11.0°C) is below minimum threshold (15°C). Loss of cell turgor.', 
 '1. Move plant to a warmer indoor location away from cold drafts. 2. Avoid cold water when watering.', 
 'Kitchen window sill');

-- 4. Sample Queries for Viva / Demonstration
-- SELECT * FROM plant_observations;
-- SELECT plant_name, stress_level, moisture_pct, temperature_c FROM plant_observations WHERE stress_level != 'Optimal Condition';
-- SELECT COUNT(*) AS total_observations, AVG(moisture_pct) AS avg_moisture, AVG(temperature_c) AS avg_temp FROM plant_observations;
