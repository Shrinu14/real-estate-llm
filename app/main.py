from rag import add_document, search
from guardrails_output import validate_output
from utils import log_info, log_error
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Real Estate Search System")
    parser.add_argument("mode", choices=["add", "search"], help="Choose add or search mode")
    parser.add_argument("text", help="The real estate-related text or query")
    args = parser.parse_args()

    if args.mode == "add":
        try:
            doc_id = add_document(args.text)
            if doc_id:
                log_info(f"Document added with ID: {doc_id}")
                print(f"Document added successfully. ID: {doc_id}")
            else:
                log_error("Failed to add document. No ID returned.")
                print("Failed to add document.")
                sys.exit(1)
        except Exception as e:
            log_error(f"Error adding document: {e}")
            print(f"Error adding document: {e}")
            sys.exit(1)

    elif args.mode == "search":
        try:
            results = search(args.text)
            if not results:
                print("No matching documents found.")
                return

            print("\nTop Matching Results:")
            for result in results:
                # Support if result is dict or string
                doc_id = result.get("id") if isinstance(result, dict) else None
                text = result.get("text") if isinstance(result, dict) else result

                if doc_id and text:
                    try:
                        validated = validate_output(doc_id, text)
                        print(f"\n✅ Document ID: {validated['id']}")
                        print(f"📄 Text: {validated['text']}")
                    except Exception as ve:
                        log_error(f"Validation failed for doc ID {doc_id}: {ve}")
                        print(f"\n⚠️ Validation failed for document ID: {doc_id}")
                else:
                    # If result is just text string
                    print(f"\n📄 Text: {text}")

        except Exception as e:
            log_error(f"Error during search: {e}")
            print(f"Error during search: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
