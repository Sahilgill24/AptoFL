module aggregator_lite::aggregation {
    use std::vector;

    // Error codes
    const EINVALID_LENGTH: u64 = 1;

    // Struct to hold the aggregated data
    struct Aggregator has key {
        data: vector<vector<u64>>,
        vector_length: u64,
    }

    // Initialize the aggregator
    public fun initialize(vector_length: u64): Aggregator {
        Aggregator {
            data: vector::empty(),
            vector_length,
        }
    }

    // Add a vector to the aggregator
    public fun add_vector(aggregator: &mut Aggregator, new_vector: vector<u64>) {
        assert!(vector::length(&new_vector) == aggregator.vector_length, EINVALID_LENGTH);
        vector::push_back(&mut aggregator.data, new_vector);
    }

    // Compute the sum of all vectors
    public fun compute_sum(aggregator: &Aggregator): vector<u64> {
        let result = vector::empty();
        let i = 0;
        while (i < aggregator.vector_length) {
            vector::push_back(&mut result, 0);
            i = i + 1;
        };

        let num_vectors = vector::length(&aggregator.data);
        i = 0;
        while (i < num_vectors) {
            let vec = vector::borrow(&aggregator.data, i);
            let j = 0;
            while (j < aggregator.vector_length) {
                let sum = *vector::borrow(&result, j) + *vector::borrow(vec, j);
                *vector::borrow_mut(&mut result, j) = sum;
                j = j + 1;
            };
            i = i + 1;
        };

        result
    }

    // Get the number of vectors added
    public fun get_num_vectors(aggregator: &Aggregator): u64 {
        vector::length(&aggregator.data)
    }

    // Get the length of vectors
    public fun get_vector_length(aggregator: &Aggregator): u64 {
        aggregator.vector_length
    }
}