#include <mosquitto.h>
#include <stdio.h>
#include <stdlib.h>
void on_connect(struct mosquitto *mqtt, void * obj,int rc)
{
    if (rc)
    {
        printf("Error with result code%d\n", rc);
        exit(-1);
    }
    mosquitto_subscribe(mqtt, NULL, "house",0);
}
void on_message(struct mosquitto* mqtt, void *obj, const struct mosquitto_message* msg)
{
    printf("New message with topic %s: %s\n",msg->topic,(char*)msg->payload);
}
int main()
{
    int rc, id=12;
    struct mosquitto* mqtt;
    mosquitto_lib_init();
    mqtt=mosquitto_new("subscribe-test",true,&id);
    //rc=mosquitto_connect(mqtt,"192.168.178.20",1883,60);
    mosquitto_connect_callback_set(mqtt,on_connect);
    mosquitto_message_callback_set(mqtt,on_message);
    
    rc=mosquitto_connect(mqtt,"localhost",1883,10);
    if (rc)
    {
        printf("couldn't connect to broker with code %d\n",rc);
        return -1;
    }
    mosquitto_loop_start(mqtt);
    printf("press Enter to quit\n");
    getchar();
    mosquitto_loop_stop(mqtt,true);

    mosquitto_disconnect(mqtt);
    mosquitto_destroy(mqtt);
    mosquitto_lib_cleanup();
    return 0;
}