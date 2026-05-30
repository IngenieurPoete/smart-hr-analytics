-- ============================================
-- Smart HR Analytics — Data Warehouse
-- Script 01 : Création de la base
-- ============================================

IF NOT EXISTS (
    SELECT name FROM sys.databases WHERE name = 'SmartHR_DW'
)
BEGIN
    CREATE DATABASE SmartHR_DW;
    PRINT 'Base SmartHR_DW créée.';
END
ELSE
    PRINT 'Base SmartHR_DW existe déjà.';

GO
USE SmartHR_DW;
GO