import asyncio
from src.medicaldb.health_profile import upsert_user_health_profile, user_health_profile_to_schema


async def main():
    uhp = await upsert_user_health_profile(
        identifier='sepehr',
        first_name='sepehr',
        last_name='yeganeh',
        age=23,
        sex='M',
    )

    ups = await user_health_profile_to_schema(uhp)

    print(ups)


if __name__ == '__main__':
    asyncio.run(main())
