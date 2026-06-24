from embeddings.vector_store import VectorStore



def main():

    store = VectorStore()

    print(store.list_collections())

    print(
        store.has_collection()
    )


if __name__ == "__main__":
    main()