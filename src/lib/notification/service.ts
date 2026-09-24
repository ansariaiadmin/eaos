export const notificationService = {
  send: async (payload: any) => {
    console.log('Notification via standard path — eaos — تاریکی روشن شد', payload);
    return [{ channel: 'in_app', success: true, messageId: `inapp-${Date.now()}`, at: new Date().toISOString() }];
  }
};
