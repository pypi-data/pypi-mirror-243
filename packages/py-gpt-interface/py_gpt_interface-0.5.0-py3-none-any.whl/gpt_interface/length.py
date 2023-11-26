import tiktoken

from gpt_interface.log import Log


def length(model: str, log: Log) -> int:
    enc = tiktoken.encoding_for_model(model)
    return sum([
        len(enc.encode(message.content)) + 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for message in log
    ]) + 2  # every reply is primed with <im_start>assistant


# TODO: prune messages when they get too long
def prune(self):
    """Prune the log to a reasonable number of tokens."""
    messages = [
        message
        for message in self.log
        if not message.persist
    ]
    messages.append(
        Message(
            role="user",
            content=(
                "Write a short summary of what we've said so far that I can give you "
                "later if we were to continue this conversation. Do not add a preamble "
                "or postamble to this summary."
            ),
        )
    )
    print("Pruning log...", Colors.alert)
    try:
        summary = "Summary of chat: " + llm_api(messages, self.model, 1)
        new_log = [
            message
            for message in self.log
            if message.persist
        ] + [Message(role="assistant", content=summary)]
        enc = tiktoken.encoding_for_model(self.model)
        new_log_length = sum([
            len(enc.encode(message.content))
            for message in new_log
        ])
        n_messages_kept = 0
        messages.pop()
        kept_messages_length = len(enc.encode(messages[-1].content))
        while kept_messages_length + new_log_length < self.after_prune_threshold:
            n_messages_kept += 1
            kept_messages_length += len(enc.encode(messages[-n_messages_kept-1].content))
        min_messages_kept = 3
        new_log += messages[-max(n_messages_kept, min_messages_kept):]
        self.log = new_log
        print("Pruning successful.\n", Colors.alert)
    except Exception:
        print("Failed to prune log.\n", Colors.alert)
