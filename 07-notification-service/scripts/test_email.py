"""
Test Email Sending

Simple script to test email functionality.
"""

import asyncio
from uuid import uuid4

from app.providers.email_provider import email_provider


async def test_email():
    """Test sending a simple email."""
    print("📧 Testing Email Provider...")
    print("-" * 60)
    
    # Test email validation
    print("\n1️⃣ Testing email validation...")
    valid = email_provider.validate_email_address("test@example.com")
    print(f"   ✅ test@example.com: {valid}")
    
    invalid = email_provider.validate_email_address("invalid-email")
    print(f"   ❌ invalid-email: {not invalid}")
    
    # Test template rendering
    print("\n2️⃣ Testing template rendering...")
    try:
        rendered = email_provider.render_template(
            template_name="welcome.html",
            variables={
                "name": "John Doe",
                "app_name": "Gravity Platform",
                "dashboard_url": "https://app.gravity.com/dashboard",
                "support_email": "support@gravity.com",
            }
        )
        print(f"   ✅ Template rendered: {len(rendered)} characters")
    except Exception as e:
        print(f"   ❌ Template rendering failed: {e}")
    
    # Test email sending (requires SMTP credentials)
    print("\n3️⃣ Testing email sending...")
    print("   ⚠️  Skipped (requires SMTP credentials)")
    print("   To test: Update .env with SMTP settings and uncomment below")
    
    # Uncomment to test real sending:
    # success = await email_provider.send_email(
    #     to="your-email@example.com",
    #     subject="Test from Gravity Notification Service",
    #     content="This is a test email",
    #     html_content="<h1>Test Email</h1><p>This is a test email from Gravity!</p>"
    # )
    # print(f"   {'✅' if success else '❌'} Email sent: {success}")
    
    print("\n" + "=" * 60)
    print("✅ Email provider tests complete!")
    print("\nTo send real emails:")
    print("1. Update .env with SMTP credentials")
    print("2. Uncomment the email sending code above")
    print("3. Run: poetry run python scripts/test_email.py")


if __name__ == "__main__":
    asyncio.run(test_email())
