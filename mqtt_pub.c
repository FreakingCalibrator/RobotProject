#include <mosquitto.h>
#include <stdio.h>

int main()
{
    char command[5];
    int rc;
    struct mosquitto* mqtt;
    mosquitto_lib_init();
    mqtt=mosquitto_new("mosquitto",true,NULL);
    rc=mosquitto_connect(mqtt,"192.168.178.27",1883,60);
    //rc=mosquitto_connect(mqtt,"localhost",1883,60);
    if (rc!=0){
        printf("client couldn't connect. Code %d\n",rc);
        mosquitto_destroy(mqtt);
        return -1;
    }
    //scanf("%c",command);
    /*while (!strcmp(command, "stop"))
    {

    }*/
    printf("we are connected now!\n");
    mosquitto_publish(mqtt,NULL, "house",6,"Hello",0,false);
    mosquitto_disconnect(mqtt);
    mosquitto_destroy(mqtt);
    mosquitto_lib_cleanup();
    return 0;
}