import time

class InactivityTracker:
    def __init__(self):
        self.activity_log = {}

    def update_activity(self, student_id, is_focused):
        current_time = time.time()
        if student_id not in self.activity_log:
            self.activity_log[student_id] = {
                "start_time": current_time,
                "last_check": current_time,
                "inactive": False
            }

        log = self.activity_log[student_id]

        if not is_focused:
            # Start inactivity period
            if not log["inactive"]:
                log["start_time"] = current_time
                log["inactive"] = True
        else:
            # Reset if focused again
            log["inactive"] = False
            log["start_time"] = current_time

        log["last_check"] = current_time

    def should_warn(self, student_id):
        if student_id not in self.activity_log:
            return False

        log = self.activity_log[student_id]
        return log["inactive"] and (time.time() - log["start_time"] >= 600)  # 10 minutes
