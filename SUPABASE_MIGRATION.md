# Supabase Migration Plan

## Step 1: Setup Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Get your project URL and anon key
4. Set up environment variables

## Step 2: Database Schema
Create these tables in Supabase:

```sql
-- User profiles table
CREATE TABLE user_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User emissions table
CREATE TABLE user_emissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    emissions DECIMAL NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User goals table
CREATE TABLE user_goals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    goals JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Step 3: Environment Variables
Add to your `.env` file:
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
```

## Step 4: Install Dependencies
```bash
pip install supabase python-dotenv
```

## Step 5: Update requirements.txt
Add:
```
supabase==2.3.4
python-dotenv==1.0.0
```

## Step 6: Migrate Data
Run a migration script to move existing SQLite data to Supabase.

## Benefits of This Migration:

### 1. **Built-in Authentication**
- No more custom password hashing
- Email verification
- Password reset functionality
- Social login options (Google, GitHub, etc.)

### 2. **Scalability**
- Handles thousands of concurrent users
- Automatic backups
- Global CDN

### 3. **Security**
- Row-level security (RLS)
- Built-in SQL injection prevention
- Regular security updates

### 4. **Development Experience**
- Real-time subscriptions
- Automatic API generation
- Built-in dashboard

### 5. **Cost**
- Free tier: Up to 50,000 monthly active users
- 500MB database storage
- 1GB file storage

## Migration Strategy:

1. **Phase 1**: Set up Supabase project and schema
2. **Phase 2**: Create migration script for existing data
3. **Phase 3**: Update authentication system
4. **Phase 4**: Test thoroughly
5. **Phase 5**: Deploy with environment variables

Would you like me to implement this migration?
