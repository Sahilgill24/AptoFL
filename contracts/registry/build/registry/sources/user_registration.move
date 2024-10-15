module registry::user_registration {
    use std::signer;
    use std::string;
    use std::error;
    use aptos_framework::event;
    #[test_only]
    use std::debug;

    // Resource to store user registration information
    struct UserRegistry has key {
        user_id: string::String,
    }

    // Event to track user registrations or updates
    #[event]
    struct UserRegistrationEvent has drop, store {
        account: address,
        old_user_id: string::String,
        new_user_id: string::String,
    }

    /// Error code when no user is registered
    const ENO_USER_REGISTERED: u64 = 100;

    // View function to get the registered user ID for an account
    #[view]
    public fun get_user_id(addr: address): string::String acquires UserRegistry {
        assert!(exists<UserRegistry>(addr), error::not_found(ENO_USER_REGISTERED));
        borrow_global<UserRegistry>(addr).user_id
    }

    // Entry function to register a new user or update an existing registration
    public entry fun register_user(account: signer, new_user_id: string::String) 
    acquires UserRegistry {
        let account_addr = signer::address_of(&account);

        // If the user is not registered, create a new registration
        if (!exists<UserRegistry>(account_addr)) {
            move_to(&account, UserRegistry {
                user_id: new_user_id,
            });
        } else {
            // Update the existing registration with a new user ID
            let old_registry = borrow_global_mut<UserRegistry>(account_addr);
            let old_user_id = old_registry.user_id;
            event::emit(UserRegistrationEvent {
                account: account_addr,
                old_user_id,
                new_user_id: copy new_user_id,
            });
            old_registry.user_id = new_user_id;
        }
    }

    // Test function to verify registration works correctly
    #[test(account = @0x1)]
    public entry fun test_user_registration(account: signer) acquires UserRegistry {
        let test_msg: string::String = string::utf8(b"Running user registration test...");
        debug::print(&test_msg);

        let addr = signer::address_of(&account);

        // Register a user for the first time
        register_user(account, string::utf8(b"User123"));

        // Assert that the user ID was set correctly
        assert!(
            get_user_id(addr) == string::utf8(b"User123"),
            ENO_USER_REGISTERED
        );

        // Update the user ID
        register_user(account, string::utf8(b"NewUser456"));

        // Assert that the user ID was updated correctly
        assert!(
            get_user_id(addr) == string::utf8(b"NewUser456"),
            ENO_USER_REGISTERED
        );
    }
}
