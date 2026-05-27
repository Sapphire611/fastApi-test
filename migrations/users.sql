create table public.users (
  id text not null,
  username character varying(20) not null,
  email character varying(255) not null,
  password character varying(255) not null,
  user_type text not null,
  profile_name text null,
  profile_phone text null,
  profile_avatar text null,
  is_active boolean null default true,
  created_at timestamp with time zone null default now(),
  updated_at timestamp with time zone null default now(),
  constraint users_pkey primary key (id),
  constraint users_email_key unique (email),
  constraint users_username_key unique (username),
  constraint users_user_type_check check (
    (
      user_type = any (array['admin'::text, 'user'::text])
    )
  )
) TABLESPACE pg_default;

create index IF not exists idx_users_email on public.users using btree (email) TABLESPACE pg_default;

create index IF not exists idx_users_username on public.users using btree (username) TABLESPACE pg_default;

create trigger update_users_updated_at BEFORE
update on users for EACH row
execute FUNCTION update_updated_at_column ();