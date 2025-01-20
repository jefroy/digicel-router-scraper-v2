-- Drop existing table
drop table if exists port_forwards cascade;

-- Create the port_forwards table with exact column names
create table port_forwards (
                               id uuid default gen_random_uuid() primary key,
                               created_at timestamp with time zone default timezone('utc'::text, now()) not null,
                               config_mode text not null,
                               external_ipv4_address text not null,
                               external_port text not null,
                               internal_port text not null,
                               protocol text not null,
                               internal_ip text not null,
                               status text not null,
                               allow_proposal text not null,
                               host_name text not null,
                               is_active boolean default true
);

-- Create indexes for better query performance
create index idx_port_forwards_host_name on port_forwards(host_name);
create index idx_port_forwards_is_active on port_forwards(is_active);
create index idx_port_forwards_internal_port on port_forwards(internal_port);

-- Create a view for active RDP forwards
create or replace view active_rdp_forwards as
select
    external_ipv4_address,
    external_port,
    internal_ip,
    host_name,
    created_at as last_updated
from port_forwards
where
    internal_port = '3389'
  and is_active = true
  and status = 'Success'
order by created_at desc;

-- Enable RLS
alter table port_forwards enable row level security;

-- Create policies
create policy "Enable read access for all users"
    on port_forwards for select
                                    using (true);

create policy "Enable insert for authenticated users"
    on port_forwards for insert
    to authenticated
    with check (true);

create policy "Enable update for service role"
    on port_forwards for update
                                           using (true);