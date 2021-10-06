from multiprocessing import Process, Event

import uvicorn


def simple_loop(event: Event) -> None:
    while True:
        print("looped!")
        if event.wait(timeout=5):
            print("break out of loop")
            break


def web_server(port: int):
    uvicorn.run("app.api:app", port=port)


def main():

    wait_event = Event()
    loop_thread = Process(target=simple_loop, args=(wait_event,))

    web_thread = Process(target=web_server, args=(8080,))
    web_thread2 = Process(target=web_server, args=(8081,))

    print("starting threads")
    loop_thread.start()
    web_thread.start()
    web_thread2.start()

    print("joining threads")

    web_thread.join()
    web_thread2.join()
    wait_event.set()

    print("exited threads")


if __name__ == "__main__":
    main()
