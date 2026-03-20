from core.robot_brain import RobotBrain


def main():
    brain = RobotBrain()
    print("Qbot is ready. Type 'quit' to exit.\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit"):
                print("Qbot: Goodbye!")
                break
            if user_input.lower() == "rest":
                print("[Forcing rest process...]")
                brain._handle_session_end()
                continue
            response = brain.chat(user_input)
            print(f"Qbot: {response}\n")

    except KeyboardInterrupt:
        print("\nQbot: Goodbye!")

    finally:
        brain.shutdown()


if __name__ == "__main__":
    main()