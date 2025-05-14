--Crear usuario Admin en Supabase:

--email: admin@folklor.com
--contraseña: adminFolk123

--Modificación en SQL para rol y nombre:
UPDATE auth.users
SET raw_app_meta_data = COALESCE(raw_app_meta_data, '{}'::jsonb) || '{"rol": "Admin"}'::jsonb
WHERE id = '49241247-2a6f-4340-910a-0b2a73658c5e';
UPDATE auth.users
SET raw_user_meta_data = COALESCE(raw_user_meta_data, '{}'::jsonb) || '{"display_name": "Juan Martinez"}'::jsonb
WHERE id = '49241247-2a6f-4340-910a-0b2a73658c5e';

--Crear usuario alumno en Supabase:

--email: gera.ramirez@folklor.com
--contraseña: geraRmz123

--Modificación en SQL para rol y nombre:
UPDATE auth.users
SET raw_app_meta_data = COALESCE(raw_app_meta_data, '{}'::jsonb) || '{"rol": "Alumno"}'::jsonb
WHERE id = '084e9a18-5c40-4d48-aaca-f6b100e9ae79';
UPDATE auth.users
SET raw_user_meta_data = COALESCE(raw_user_meta_data, '{}'::jsonb) || '{"display_name": "Gerardo Ramirez"}'::jsonb
WHERE id = '084e9a18-5c40-4d48-aaca-f6b100e9ae79';
