
CREATE SCHEMA IF NOT EXISTS phyllo_schema;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- common tables
CREATE TABLE IF NOT EXISTS phyllo_schema.common (
	id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
	last_updated_by_user character varying(36),
    last_updated_at_user timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_updated_by_sys character varying(36),
    last_updated_at_sys timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by_user character varying(36),
    created_at_user timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
ALTER TABLE phyllo_schema.common OWNER TO phyllo;


-- global tables
CREATE TABLE IF NOT EXISTS phyllo_schema.data_platform (
	name character varying(100) NOT NULL,
	url character varying(2048) NOT NULL,
	logo_url character varying(2048),
	is_oauth_supported boolean DEFAULT false NOT NULL,
	is_uname_pwd_supported boolean DEFAULT false NOT NULL,
	CONSTRAINT pkey_data_platform_id PRIMARY KEY(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.data_platform OWNER TO phyllo;


-- op_name enum = fill | click | check | uncheck | fetch | verify | save-mfa-session | save-login-session | open-browser | close-browser | navigate-url | verify-and-fork | operaton-completed | operaton-in-progress |
CREATE TABLE IF NOT EXISTS phyllo_schema.dp_login_path (
	data_platform_id uuid NOT NULL,
	level character varying(100) NOT NULL,
	sequence_no int NOT NULL,
	element_identifier character varying(500),
	op_name character varying(50) NOT NULL, 
	element_key_name character varying(100),
	element_key_value character varying(2048),
	CONSTRAINT pkey_dp_login_path_id PRIMARY KEY(id),
	CONSTRAINT fkey_dp_login_path_data_platform_id FOREIGN KEY(data_platform_id) REFERENCES phyllo_schema.data_platform(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.dp_login_path OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.dp_employer_info (
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.dp_employer_info OWNER TO phyllo;


-- tenant tables
CREATE TABLE IF NOT EXISTS phyllo_schema.tenant (
	name character varying(200) NOT NULL,
	url character varying(2048) NOT NULL,
	logo_url character varying(2048),
	domain_name character varying(200) NOT NULL,
	status character varying(50) NOT NULL, -- activated | deactivated | pending
	CONSTRAINT pkey_tenant_id PRIMARY KEY(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.tenant OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.tenant_credential (
	tenant_id uuid NOT NULL,
	api_key character varying(100) NOT NULL,
	api_secret character varying(2048) NOT NULL,
	sdk_token character varying(100) NOT NULL,
	access_token character varying(2048),
	CONSTRAINT pkey_tenant_credential_id PRIMARY KEY(id),
	CONSTRAINT fkey_tenant_credential_tenant_id FOREIGN KEY(tenant_id) REFERENCES phyllo_schema.tenant(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.tenant_credential OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.applicant (
	tenant_id uuid NOT NULL,
	applicant_identifier character varying(100) NOT NULL,
	UNIQUE(tenant_id, applicant_identifier),
	CONSTRAINT pkey_applicant_id PRIMARY KEY(id),
	CONSTRAINT fkey_applicant_tenant_id FOREIGN KEY(tenant_id) REFERENCES phyllo_schema.tenant(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.applicant OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.dp_applicant_login_info (
	tenant_id uuid NOT NULL,
	data_platform_id uuid NOT NULL,
	applicant_id uuid NOT NULL,
	username character varying(100),
	pwd character varying(512),
	is_mfa_enabled Boolean DEFAULT false NOT NULL,
	login_type character varying(100), -- uname-pwd | google | facebook | apple
	mfa_url character varying(2048),
	mfa_cookies character varying,
	login_url character varying(2048),
	login_cookies character varying,
	login_status character varying(100), -- none | in-progress | completed
	resume_from character varying(100),
	session_id character varying,
	--UNIQUE(data_platform_id, applicant_id),
	CONSTRAINT pkey_dp_applicant_login_info_id PRIMARY KEY(id),
	CONSTRAINT fkey_applicant_tenant_id FOREIGN KEY(tenant_id) REFERENCES phyllo_schema.tenant(id),
	CONSTRAINT fkey_dp_applicant_login_info_data_platform_id FOREIGN KEY(data_platform_id) REFERENCES phyllo_schema.data_platform(id),
	CONSTRAINT fkey_dp_applicant_login_info_applicant_id FOREIGN KEY(applicant_id) REFERENCES phyllo_schema.applicant(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.dp_applicant_login_info OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.applicant_book_info (
	tenant_id uuid NOT NULL,
	applicant_id uuid NOT NULL,
	name character varying(100) NOT NULL,
	UNIQUE(applicant_id, name),
	CONSTRAINT pkey_applicant_book_info_id PRIMARY KEY(id),
	CONSTRAINT fkey_applicant_book_info_tenant_id FOREIGN KEY(tenant_id) REFERENCES phyllo_schema.tenant(id),
	CONSTRAINT fkey_applicant_book_info_applicant_id FOREIGN KEY(applicant_id) REFERENCES phyllo_schema.applicant(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.dp_applicant_login_info OWNER TO phyllo;


CREATE TABLE IF NOT EXISTS phyllo_schema.applicant_doc_info (
	tenant_id uuid NOT NULL,
	applicant_id uuid NOT NULL,
	book_id uuid NOT NULL,
	name character varying(100) NOT NULL,
	path character varying(100) NOT NULL,
	type character varying(100) NOT NULL,
	CONSTRAINT pkey_applicant_doc_info_id PRIMARY KEY(id),
	CONSTRAINT fkey_applicant_doc_info_tenant_id FOREIGN KEY(tenant_id) REFERENCES phyllo_schema.tenant(id),
	CONSTRAINT fkey_applicant_doc_info_applicant_id FOREIGN KEY(applicant_id) REFERENCES phyllo_schema.applicant(id),
	CONSTRAINT fkey_applicant_doc_info_book_id FOREIGN KEY(book_id) REFERENCES phyllo_schema.applicant_book_info(id)
) INHERITS (phyllo_schema.common);
ALTER TABLE phyllo_schema.dp_applicant_login_info OWNER TO phyllo;


-- upwork
INSERT INTO phyllo_schema.data_platform(id, name, url, logo_url, is_oauth_supported, is_uname_pwd_supported) VALUES
('034181db-f4f9-426b-b9ee-83a66fd42c6d', 'upwork', 'https://www.upwork.com', NULL, true, true) ON CONFLICT DO NOTHING;

-- upwork login path
INSERT INTO phyllo_schema.dp_login_path(data_platform_id, level, sequence_no, element_identifier, op_name, element_key_name, element_key_value)
VALUES
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1', 1, NULL, 'navigate-url', 'login-url', 'https://www.upwork.com/ab/account-security/login'),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1', 2, 'xpath=//a[text()=''Upwork'']', 'verify', 'element', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1', 3, 'id=login_username', 'fill', 'username', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1', 4, 'id=login_password_continue', 'click', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1', 5, '{"id=login_password": "1.1", "id=login_control_submit": "1.2"}', 'verify-and-fork', NULL, NULL),

('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1', 1, 'id=login_password', 'fill', 'password', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1', 2, 'xpath=//input[@id=''login_rememberme'']/following-sibling::span', 'check', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1', 3, 'id=login_control_continue', 'click', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1', 4, '{"xpath=//img[contains(@class,''nav-avatar nav-user-avatar'')]": "1.1.1", "xpath=//h2[text()=''Confirm that it''s you'']": "1.1.2"}', 'verify-and-fork', NULL, NULL),

('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.2', 1, 'id=login_control_submit', 'click', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.2', 2, NULL, 'google-login', NULL, NULL),
--('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.2', 3, NULL, 'save-login-session', NULL, NULL),
--('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.2', 4, NULL, 'operation-completed', NULL, NULL),
--('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.2', 5, NULL, 'close-window', NULL, NULL),

('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.1', 1, NULL, 'save-login-session', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.1', 2, NULL, 'operation-completed', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.1', 3, NULL, 'close-window', NULL, NULL),

('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.2', 1, NULL, 'save-mfa-session', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.2', 2, NULL, 'operation-in-progress', 'resume-from', '2'),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '1.1.2', 3, NULL, 'close-window', NULL, NULL),

('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 1, NULL, 'load-mfa-session', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 2, 'xpath=//h2[text()=''Confirm that it''s you'']', 'verify', 'element', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 3, 'id=login_deviceAuthOtp_otp', 'fill', 'otp', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 4, 'id=login_deviceAuthOtp_remember', 'check', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 5, 'id=login_control_continue', 'click', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 6, 'xpath=//img[contains(@class,''nav-avatar nav-user-avatar'')]', 'verify', 'element', NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 7, NULL, 'save-login-session', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 8, NULL, 'operation-completed', NULL, NULL),
('034181db-f4f9-426b-b9ee-83a66fd42c6d', '2', 9, NULL, 'close-window', NULL, NULL)
 ON CONFLICT DO NOTHING;


INSERT INTO phyllo_schema.tenant(id, name, url, logo_url, domain_name, status) VALUES
('fc14a17d-0667-4bd6-856e-b4aaec68984c', 'phyllo', 'https://getphyllo.com', NULL, 'getphyllo.com', 'ACTIVATED');


INSERT INTO phyllo_schema.tenant_credential(tenant_id, api_key, api_secret, sdk_token, access_token) VALUES
('fc14a17d-0667-4bd6-856e-b4aaec68984c', 'api_key', 'api_secret', 'sdk_token', 'access_token');


INSERT INTO phyllo_schema.applicant(id, tenant_id, applicant_identifier) VALUES
('c1af9c06-2c9e-4de0-9745-cbf36bc1be0f', 'fc14a17d-0667-4bd6-856e-b4aaec68984c', '5a3ab477-1be8-4b37-9e61-a51174c40d09');


-- udemy
INSERT INTO phyllo_schema.data_platform(id, name, url, logo_url, is_oauth_supported, is_uname_pwd_supported) VALUES
('199a2144-c599-4e06-84f4-d18836127a6b', 'udemy', 'https://www.udemy.com', NULL, true, true) ON CONFLICT DO NOTHING;

-- udemy login path
INSERT INTO phyllo_schema.dp_login_path(data_platform_id, level, sequence_no, element_identifier, op_name, element_key_name, element_key_value)
VALUES
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 1, NULL, 'navigate-url', 'login-url', 'https://www.udemy.com/join/login-popup'),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 2, 'xpath=//a[text()=''Udemy'']', 'verify', 'element', NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 3, 'id=form-item-email', 'fill', 'username', NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 4, 'id=form-item-password', 'fill', 'password', NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 5, 'id=submit-id-submit', 'click', NULL, NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 6, 'xpath=//a[text()=''Udemy'']', 'verify', 'element', NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 7, NULL, 'save-login-session', NULL, NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 8, NULL, 'operation-completed', NULL, NULL),
('199a2144-c599-4e06-84f4-d18836127a6b', '1', 9, NULL, 'close-window', NULL, NULL)
ON CONFLICT DO NOTHING;


-- slack
INSERT INTO phyllo_schema.data_platform(id, name, url, logo_url, is_oauth_supported, is_uname_pwd_supported) VALUES
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', 'slack', 'https://phyllo.slack.com', NULL, true, true) ON CONFLICT DO NOTHING;

-- slack login path
INSERT INTO phyllo_schema.dp_login_path(data_platform_id, level, sequence_no, element_identifier, op_name, element_key_name, element_key_value)
VALUES
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1', 1, NULL, 'navigate-url', 'login-url', 'https://phyllo.slack.com/'),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1', 2, 'id=email', 'fill', 'username', NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1', 3, 'id=password', 'fill', 'password', NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1', 4, 'id=signin_btn', 'click', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1', 5, '{"xpath=//*[@id=''page_contents'']/div/div/div[2]/h1]": "1.1", "xpath=//*[@id=''page_contents'']/div/div[2]/form/div/input": "1.2"}', 'verify-and-fork', NULL, NULL),

('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.1', 1, NULL, 'save-login-session', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.1', 2, NULL, 'operation-completed', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.1', 3, NULL, 'close-window', NULL, NULL),

('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.2', 1, NULL, 'save-mfa-session', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.2', 2, NULL, 'operation-in-progress', 'resume-from', '2'),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '1.2', 3, NULL, 'close-window', NULL, NULL),

('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 1, NULL, 'load-mfa-session', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 2, 'xpath=//*[@id=''page_contents'']/div/div[2]/form/div/input', 'fill', 'otp', NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 3, 'id=signin_btn', 'click', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 4, 'https://phyllo.slack.com/ssb/redirect?entry_point=workspace_signin', 'verify', 'url', NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 5, NULL, 'save-login-session', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 6, NULL, 'operation-completed', NULL, NULL),
('a2a35c6c-fc3c-40c5-b503-9cdecf889bba', '2', 7, NULL, 'close-window', NULL, NULL)
ON CONFLICT DO NOTHING;

